const awsConfig = {
  Auth: {
    // REQUIRED - Amazon Cognito Region
    region: "eu-west-2",

    // OPTIONAL - Amazon Cognito User Pool ID
    userPoolId: "eu-west-2_n6vDQdu5N",

    // OPTIONAL - Amazon Cognito Web Client ID (26-char alphanumeric string)
    userPoolWebClientId: "cncih8g9fhdcnirv8q3vjht7g",

    // OPTIONAL - Hosted UI configuration
    oauth: {
      // Your Cognito domain, **without** the https:// prefix
      domain: "eu-west-2n6vdqdu5n.auth.eu-west-2.amazoncognito.com",

      // Scopes you want authorization for
      scope: ["email", "openid", "phone"],

      // Callback URL(s) after sign in/out
      redirectSignIn: "http://localhost:5173/",
      redirectSignOut: "http://localhost:5173/",

      // OAuth grant type
      responseType: "code",
    },
  },
};

export default awsConfig;
