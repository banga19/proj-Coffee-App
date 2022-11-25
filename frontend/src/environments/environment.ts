/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-ghmo5g35rrbody4g.us',
    audience: 'identity access app', // the audience set for the auth0 app
    clientId: 'SBwI8tahkMhqR6gqO6ZdZJk8QfbxxKCa', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', // the base url of the running ionic application. 
  }
};
