const awsConfig = {
  region: "eu-west-2",
  userPoolId: "eu-west-2_n6vDQdu5N",
  userPoolWebClientId: "cncih8g9fhdcnirv8q3vjht7g",
  oauth: {
    domain: "https://eu-west-2n6vdqdu5n.auth.eu-west-2.amazoncognito.com",
    scope: ["email", "openid", "phone"],
    redirectSignIn: "http://localhost:5173/",
    redirectSignOut: "http://localhost:5173/",
    responseType: "code"
  }
};

export default awsConfig;
