const Mock = require('mockjs')
const mockdata = Mock.mock({
  'data|100': [
    {
      name: '@name',
      ip: '@ip',
      port: '@integer(1,65535)',
      topdomain: '@domain',
      subdomain: 'test.@domain',
      title: '@word',
      type: 'rce',
      plugin: 'nuclei',
      info: '@sentence(10,100)',
      req: 'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n',
      resp: '200 OK\r\nContent-Length: 10\r\n\r\nhelloworld',
      'tag|1-3': ['@word'],
      created: '2022-04-05'
    }
  ]
})
module.exports = [
  {
    url: '/api/vuldata',
    type: 'post',
    response: config => {
      const body = config.body
      body.page = body.page ? body.page : 1
      const start = (body.page - 1) * body.size
      const response = {
        success: true,
        'total': mockdata.data.length,
        'data': [],
        'size': body.size,
        'currentpage': body.currentpage,
        'page': (mockdata.data.length - mockdata.data.length % body.size) / body.size
      }
      if (start > mockdata.data.length) {
        return response
      }
      for (var i = 0; i < body.size; i++) {
        if (start + i >= mockdata.data.length) { break }
        response.data.push(mockdata.data[start + i])
      }
      const sortfunc = (col, desc) => {
        return function(a, b) {
          if (col === '') {
            col = 'created'
          }
          a = a[col]
          b = b[col]
          let result = 0
          if (a > b) {
            result = 1
          } else if (a < b) {
            result = -1
          } else {
            result = 0
          }
          if (desc) {
            result = -result
          }
          return result
        }
      }
      response.data = response.data.sort(sortfunc(body.sort, body.desc))
      return response
    }
  }
]
