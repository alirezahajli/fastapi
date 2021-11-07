exports.config = {
  tests: './scenarios/**/*_test.js',
  output: './output',
  timeout: 1000000,
  helpers: {
    // WebDriver: {
    //   url: 'https://opencollective.com',
    //   browser: 'chrome',
    //   restart: false,
    //   maximize: true,
    //   keepCookies: true,
    //   show: true
    // },
    REST: {
      endpoint: 'http://127.0.0.1:8000',
      defaultHeaders: {
        "Content-Type": "application/json"
      }
    }
  },
  plugins: {
    allure: {
      enabled: true
    }
  },
  bootstrap: null,
  mocha: {
    reporterOptions: {
      mochaFile: './result.xml'
    }
  },
  name: 'codeceptjs'
}
