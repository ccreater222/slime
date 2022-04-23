const Mock = require('mockjs')
const data = {
  'name': '@word',
  'topdomain': '@domain',
  'subdomain': 'test.@topdomain',
  'iscdn': '@bool',
  'ip': '@ip',
  'port': '@integer(1,65535)',
  'service': '@protocol',
  'req': 'GET / HTTP/1.1\r\nHost: 127.0.0.1\r\n\r\n',
  'resp': '200 OK\r\n\r\nTest',
  'info': {
    'title': '@sentence(10,20)',
    'bannner': '@sentence(10,20)',
    'screenshot': 'https://101.35.113.48:60443/api/image/625f8bb55163010023719077/https_bot.ccreater.top_8443.jpg',
    'sslname': 'name'
  },
  'finger': [
    '@word'
  ],
  'tag': [
    '@word'
  ],
  'created': '@datetime',
  'updated': '@datetime',
  'taskid': '@guid'
}
const mockdata = Mock.mock({
  'data|100': [data]
})
module.exports = [
  {
    url: '/api/service',
    type: 'post',
    response: config => {
      const body = config.body
      const columns = body.columns ? body.columns : Object.keys(mockdata.data[0])
      body.page = body.page ? body.page : 1
      const start = (body.page - 1) * body.size
      var response = {
        'success': true,
        'total': mockdata.data.length,
        'data': {
          'columns': columns,
          'columndatas': []
        },
        'size': body.size,
        'currentpage': body.currentpage,
        'page': (mockdata.data.length - mockdata.data.length % body.size) / body.size
      }
      if (start > mockdata.data.length) {
        return response
      }
      for (var i = 0; i < body.size; i++) {
        if (start + i >= mockdata.data.length) { break }
        var tempdata = {}
        columns.forEach(e => {
          tempdata[e] = mockdata.data[start + i][e]
        })
        response.data.columndatas.push(tempdata)
      }
      const sortfunc = (col, desc) => {
        return function(a, b) {
          if (col === '') {
            col = 'id'
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
      response.data.columndatas = response.data.columndatas.sort(sortfunc(body.sort, body.desc))
      return response
    }
  }
]
