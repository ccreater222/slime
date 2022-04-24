const Mock = require('mockjs')
const mockdata = Mock.mock({
  comparedata: {
    'resource|7': ['@integer(1,100)'],
    'vul|7': ['@integer(1,100)'],
    'task|7': ['@integer(1,100)']
  },
  countdata: {
    resource: '@integer(1,100)',
    service: '@integer(1,100)',
    task: '@integer(1,100)',
    vul: '@integer(1,100)'
  }
})
module.exports = [
  {
    url: '/api/dashboard',
    type: 'get',
    response: config => {
      return {
        success: true,
        data: mockdata
      }
    }
  }
]
