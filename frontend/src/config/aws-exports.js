// AWS Amplify Configuration for KairoCal
// This file contains the Cognito configuration for authentication

const awsExports = {
  aws_project_region: "eu-west-2",
  aws_cognito_region: "eu-west-2",
  aws_user_pools_id: "eu-west-2_n6vDQdu5N",
  aws_user_pools_web_client_id: "cncih8g9fhdcnirv8q3vjht7g",
  oauth: {
    domain: "eu-west-2n6vdqdu5n.auth.eu-west-2.amazoncognito.com",
    scope: ["email", "openid", "phone"],
    redirectSignIn: "http://localhost:5173/",
    redirectSignOut: "http://localhost:5173/",
    responseType: "code"
  }
};

export default awsExports;