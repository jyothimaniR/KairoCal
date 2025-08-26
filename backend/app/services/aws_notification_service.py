# AWS SES & SNS Notification Service for KairoCal
import boto3
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AWSNotificationService:
    """Enhanced notification service with AWS SES (Email) and SNS (SMS/Push)"""
    
    def __init__(self):
        # Initialize AWS clients
        self.ses_client = boto3.client('ses', region_name='us-east-1')
        self.sns_client = boto3.client('sns', region_name='us-east-1')
        
        # Email templates
        self.email_templates = {
            'conflict_detected': {
                'subject': '🚨 KairoCal: Schedule Conflict Detected',
                'template': 'conflict_email_template.html'
            },
            'high_priority_event': {
                'subject': '⚡ KairoCal: Critical Event Alert',
                'template': 'priority_email_template.html'
            },
            'voice_transcription_ready': {
                'subject': '🎤 KairoCal: Voice Event Created',
                'template': 'voice_email_template.html'
            },
            'bert_classification_complete': {
                'subject': '🧠 KairoCal: Event Priority Classified',
                'template': 'bert_email_template.html'
            }
        }
    
    async def send_conflict_notification(self, user_data: Dict[str, Any], conflict_data: Dict[str, Any]):
        """Send multi-channel conflict notification"""
        try:
            # 1. Real-time WebSocket (existing)
            await self._broadcast_websocket_notification(user_data['id'], 'conflict_detected', conflict_data)
            
            # 2. Email via AWS SES
            if user_data.get('email_notifications', True):
                await self._send_ses_email(
                    user_data['email'],
                    'conflict_detected',
                    conflict_data
                )
            
            # 3. SMS via AWS SNS (for high priority conflicts)
            if conflict_data.get('priority_level', 0) >= 4 and user_data.get('phone_number'):
                await self._send_sns_sms(
                    user_data['phone_number'],
                    f"🚨 URGENT: Schedule conflict detected between '{conflict_data['event1']['title']}' and '{conflict_data['event2']['title']}'. Check KairoCal for resolution."
                )
            
            # 4. In-app notification (existing)
            await self._add_in_app_notification(user_data['id'], 'conflict', conflict_data)
            
            logger.info(f"✅ Multi-channel conflict notification sent to user {user_data['id']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to send conflict notification: {e}")
    
    async def send_bert_priority_notification(self, user_data: Dict[str, Any], priority_data: Dict[str, Any]):
        """Send BERT classification result notification"""
        try:
            # 1. Real-time WebSocket update
            await self._broadcast_websocket_notification(user_data['id'], 'priority_classified', priority_data)
            
            # 2. Email for high-confidence classifications
            if priority_data.get('confidence', 0) > 0.9 and priority_data.get('priority', 0) >= 4:
                await self._send_ses_email(
                    user_data['email'],
                    'bert_classification_complete',
                    priority_data
                )
            
            # 3. Push notification via SNS for critical events
            if priority_data.get('priority', 0) == 5:  # Critical priority
                await self._send_sns_push(
                    user_data.get('device_token'),
                    f"🔥 CRITICAL EVENT: '{priority_data['event_text']}' classified as Priority 5 with {priority_data['confidence']:.0%} confidence"
                )
            
            logger.info(f"✅ BERT priority notification sent to user {user_data['id']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to send BERT notification: {e}")
    
    async def send_voice_transcription_notification(self, user_data: Dict[str, Any], voice_data: Dict[str, Any]):
        """Send voice processing result notification"""
        try:
            # 1. Real-time WebSocket
            await self._broadcast_websocket_notification(user_data['id'], 'voice_transcription', voice_data)
            
            # 2. Email summary
            await self._send_ses_email(
                user_data['email'],
                'voice_transcription_ready',
                voice_data
            )
            
            logger.info(f"✅ Voice transcription notification sent to user {user_data['id']}")
            
        except Exception as e:
            logger.error(f"❌ Failed to send voice notification: {e}")
    
    async def _send_ses_email(self, email: str, template_type: str, data: Dict[str, Any]):
        """Send email via AWS SES"""
        try:
            template_config = self.email_templates[template_type]
            
            # Generate email body from template
            email_body = self._generate_email_body(template_type, data)
            
            response = self.ses_client.send_email(
                Source='notifications@kairocal.com',
                Destination={'ToAddresses': [email]},
                Message={
                    'Subject': {'Data': template_config['subject']},
                    'Body': {
                        'Html': {'Data': email_body},
                        'Text': {'Data': self._generate_text_body(template_type, data)}
                    }
                }
            )
            
            logger.info(f"📧 SES email sent to {email}: {response['MessageId']}")
            
        except Exception as e:
            logger.error(f"❌ SES email failed: {e}")
    
    async def _send_sns_sms(self, phone_number: str, message: str):
        """Send SMS via AWS SNS"""
        try:
            response = self.sns_client.publish(
                PhoneNumber=phone_number,
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            
            logger.info(f"📱 SNS SMS sent to {phone_number}: {response['MessageId']}")
            
        except Exception as e:
            logger.error(f"❌ SNS SMS failed: {e}")
    
    async def _send_sns_push(self, device_token: str, message: str):
        """Send push notification via AWS SNS"""
        try:
            if not device_token:
                return
            
            # Platform-specific message formatting
            message_payload = {
                'default': message,
                'APNS': json.dumps({
                    'aps': {
                        'alert': message,
                        'badge': 1,
                        'sound': 'default'
                    }
                }),
                'GCM': json.dumps({
                    'data': {
                        'message': message,
                        'title': 'KairoCal Alert'
                    }
                })
            }
            
            response = self.sns_client.publish(
                TargetArn=device_token,
                Message=json.dumps(message_payload),
                MessageStructure='json'
            )
            
            logger.info(f"🔔 SNS push sent: {response['MessageId']}")
            
        except Exception as e:
            logger.error(f"❌ SNS push failed: {e}")
    
    def _generate_email_body(self, template_type: str, data: Dict[str, Any]) -> str:
        """Generate HTML email body from template"""
        if template_type == 'conflict_detected':
            return f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #dc2626;">🚨 Schedule Conflict Detected</h2>
                <p>Your KairoCal AI system has detected a scheduling conflict:</p>
                <div style="background: #fef2f2; padding: 15px; border-left: 4px solid #dc2626;">
                    <strong>Event 1:</strong> {data.get('event1', {}).get('title', 'Unknown')}<br>
                    <strong>Event 2:</strong> {data.get('event2', {}).get('title', 'Unknown')}<br>
                    <strong>Overlap Time:</strong> {data.get('overlap_duration', 'Unknown')} minutes
                </div>
                <p><a href="https://kairocal.com/conflicts" style="background: #dc2626; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Resolve Conflict</a></p>
            </body>
            </html>
            """
        elif template_type == 'bert_classification_complete':
            return f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #059669;">🧠 BERT Priority Classification Complete</h2>
                <p>Your event has been automatically classified:</p>
                <div style="background: #ecfdf5; padding: 15px; border-left: 4px solid #059669;">
                    <strong>Event:</strong> {data.get('event_text', 'Unknown')}<br>
                    <strong>Priority Level:</strong> {data.get('priority', 'Unknown')} / 5<br>
                    <strong>Confidence:</strong> {data.get('confidence', 0):.0%}<br>
                    <strong>Method:</strong> {data.get('method', 'BERT Neural Network')}
                </div>
                <p>This classification was performed by our advanced BERT neural network trained on 15,000+ calendar events.</p>
            </body>
            </html>
            """
        return "<p>Notification from KairoCal</p>"
    
    def _generate_text_body(self, template_type: str, data: Dict[str, Any]) -> str:
        """Generate plain text email body"""
        if template_type == 'conflict_detected':
            return f"""
            Schedule Conflict Detected
            
            Your KairoCal AI system has detected a scheduling conflict:
            Event 1: {data.get('event1', {}).get('title', 'Unknown')}
            Event 2: {data.get('event2', {}).get('title', 'Unknown')}
            Overlap: {data.get('overlap_duration', 'Unknown')} minutes
            
            Visit https://kairocal.com/conflicts to resolve this conflict.
            """
        return "Notification from KairoCal AI Calendar System"

# Integration with existing WebSocket system
aws_notification_service = AWSNotificationService()
