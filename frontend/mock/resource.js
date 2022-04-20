const Mock = require('mockjs')
const data = {
  'name': '@word',
  'topdomain': '@domain',
  'subdomain': 'test.@topdomain',
  'iscdn': '@bool',
  'ip': '@ip',
  'port': '@integer(1,65535)',
  'service': '@protocol',
  'info': {
    'title': '@sentence(10,20)',
    'bannner': '@sentence(10,20)',
    'screenshot': 'https://101.35.113.48:60443/api/image/625f8bb55163010023719077/https_bot.ccreater.top_8443.jpg',
    'ssl': {
      'name': '@sentence(10,20)'
    }
  },
  'headers': {
    'content-type': 'text/html',
    'server': 'test'
  },
  'finger': [
    '@word'
  ],
  'tag': [
    '@word'
  ],
  'created': '@datetime',
  'updated': '@datetime'
}
const mockdata = Mock.mock({
  'data|100': [data]
})
module.exports = [
  {
    url: '/api/resource',
    type: 'post',
    response: config => {
      const body = config.body
      const columes = body.columes ? body.columes : ['name', 'topdomain', 'subdomain', 'iscdn', 'ip', 'port', 'service', 'info']
      const start = (config.body.page - 1) * config.body.size
      const response = {
        'success': true,
        'total': mockdata.data.length,
        'data': {
          'columes': columes,
          'columedatas': []
        },
        'size': body.size,
        'currentpage': body.currentpage,
        'page': (mockdata.data.length - mockdata.data.length % body.size) / body.size
      }
      if (start > mockdata.data.length) {
        return response
      }
      for (var i = 0; i < body.size; i++) {
        if (start + i > mockdata.data.length) break
        var tempdata = {}
        columes.forEach(e => {
          tempdata[e] = mockdata.data[start + i][e]
        })
        response.data.columedatas.push(tempdata)
      }
      return response
    }
  }
]
