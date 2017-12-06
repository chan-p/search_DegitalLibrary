const config_ = require('./' + process.env.NODE_ENV);

export default class Config {
   static get API_ORIGIN() {
     return config_.API_ORIGIN;
   }
}
