// Fixed conflict detection function for ConflictDetectionPanel.tsx
const analyzeConflictsFixed = (events: any[]): DetectedConflict[] => {
  console.log('🔍 DEBUGGING: Analyzing conflicts for events:', events.length);
  console.log('🔍 RAW EVENTS DATA:', events.map(e => ({ 
    title: e.title, 
    start: e.start_time, 
    end: e.end_time,
    all_day: e.all_day, 
    is_all_day: e.is_all_day 
  })));
  
  const conflicts: DetectedConflict[] = [];
  const timeEvents: ConflictEvent[] = [];

  // Filter out all-day events and prepare time-based events
  events.forEach(event => {
    if (!event.start_time) {
      console.log('⚠️ Event missing start_time:', event);
      return;
    }
    
    const isAllDay = (event as any).all_day || (event as any).is_all_day;
    console.log(`📝 Processing event "${event.title}" - All day: ${isAllDay}, Start: ${event.start_time}, End: ${event.end_time}`);
    
    if (isAllDay) {
      console.log(`📅 Skipping all-day event: ${event.title}`);
      return;
    }
    
    timeEvents.push({
      id: event.id,
      title: event.title,
      start_time: event.start_time,
      end_time: event.end_time, 
      priority_level: event.priority_level || 3,
      created_via: event.created_via || 'manual'
    });
  });

  console.log('⏰ DEBUGGING: Time-based events to check for conflicts:', timeEvents.length);
  timeEvents.forEach(event => {
    console.log(`  - "${event.title}": ${event.start_time} to ${event.end_time}`);
  });

  // Check for overlapping events using proper time overlap logic
  const conflictPairs: Array<ConflictEvent[]> = [];
  
  for (let i = 0; i < timeEvents.length; i++) {
    for (let j = i + 1; j < timeEvents.length; j++) {
      const event1 = timeEvents[i];
      const event2 = timeEvents[j];
      
      const start1 = new Date(event1.start_time);
      const end1 = new Date(event1.end_time);
      const start2 = new Date(event2.start_time);  
      const end2 = new Date(event2.end_time);
      
      console.log(`🔄 CHECKING OVERLAP between:`);
      console.log(`   Event 1: "${event1.title}" (${start1.toLocaleString()} - ${end1.toLocaleString()})`);
      console.log(`   Event 2: "${event2.title}" (${start2.toLocaleString()} - ${end2.toLocaleString()})`);
      
      // Check for time overlap: events overlap if start1 < end2 AND start2 < end1
      const hasOverlap = start1 < end2 && start2 < end1;
      
      console.log(`   Overlap check: ${start1.toISOString()} < ${end2.toISOString()} = ${start1 < end2}`);
      console.log(`   Overlap check: ${start2.toISOString()} < ${end1.toISOString()} = ${start2 < end1}`);
      console.log(`   RESULT: ${hasOverlap ? '🚨 CONFLICT DETECTED!' : '✅ No conflict'}`);
      
      if (hasOverlap) {
        conflictPairs.push([event1, event2]);
        console.log(`🆕 Added conflict pair: ${event1.title} vs ${event2.title}`);
      }
    }
  }

  console.log('🗂️ DEBUGGING: Found conflict pairs:', conflictPairs.length);
  conflictPairs.forEach((pair, idx) => {
    console.log(`  Pair ${idx + 1}: ${pair.map(e => e.title).join(' vs ')}`);
  });

  // Convert conflict pairs to DetectedConflict objects
  conflictPairs.forEach((eventPair, index) => {
    const timeSlot = eventPair[0].start_time.substring(0, 16);
    const groupKey = `conflict-pair-${index}-${eventPair.map(e => e.id).sort().join('-')}`;
    
    console.log(`⚠️ Creating conflict for pair at ${timeSlot}:`, eventPair.map(e => e.title));
    
    const highestPriority = Math.max(...eventPair.map(e => e.priority_level));
    const severity = highestPriority >= 4 ? 'high' : highestPriority >= 3 ? 'medium' : 'low';
    
    const conflict: DetectedConflict = {
      id: groupKey,
      conflictTime: timeSlot,
      events: eventPair,
      severity,
      suggestedResolution: `Resolve conflict between "${eventPair[0].title}" and "${eventPair[1].title}"`,
      alternativeTimes: ['2:45 PM', '4:45 PM', '5:45 PM'], // Sample times
      bertAnalysis: {
        method: 'overlap_analysis_fixed',
        confidence: 0.95,
        reasoning: `Time overlap detected between: ${eventPair.map(e => e.title).join(' and ')}`,
        isBertPowered: false
      }
    };
    
    console.log(`✅ Created conflict object:`, conflict);
    conflicts.push(conflict);
  });

  console.log(`🎯 FINAL RESULT: Found ${conflicts.length} conflicts total`);
  conflicts.forEach(conflict => {
    console.log(`  - ${conflict.id}: ${conflict.events.map(e => e.title).join(' vs ')}`);
  });
  
  return conflicts.sort((a, b) => {
    const severityOrder = { high: 3, medium: 2, low: 1 };
    return severityOrder[b.severity] - severityOrder[a.severity];
  });
};
