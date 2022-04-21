const Mock = require('mockjs')
const data = {
  'id|+1': 1,
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
    },
    'headers': {
      'content-type': 'text/html',
      'server': 'test'
    }
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
      const columes = body.columes ? body.columes : ['id', 'name', 'topdomain', 'subdomain', 'iscdn', 'ip', 'port', 'service', 'tag', 'finger', 'updated']
      body.page = body.page ? body.page : 1
      const start = (body.page - 1) * body.size
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
        if (start + i >= mockdata.data.length) { break }
        var tempdata = {}
        columes.forEach(e => {
          tempdata[e] = mockdata.data[start + i][e]
        })
        response.data.columedatas.push(tempdata)
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
      response.data.columedatas = response.data.columedatas.sort(sortfunc(body.sort, body.desc))
      return response
    }
  },
  {
    url: '/api/update/resource',
    type: 'post',
    response: function(config) {
      return { success: true }
    }
  },
  {
    url: '/api/create/resource',
    type: 'post',
    response: function(config) {
      return { success: true }
    }
  },
  {
    url: '/api/delete/resource',
    type: 'post',
    response: function(config) {
      return { success: true }
    }
  },
  {
    url: '/api/analyze/resource',
    type: 'post',
    response: function(config) {
      var target = config.body.target
      var response = {
        success: true,
        data: null
      }
      var num = 10000
      if (config.body.limit !== -1) {
        num = config.body.limit
      }
      var numstr = `data|${num}`
      target = 'cidr'
      if (target === 'cidr') {
        var tpl = {}
        tpl[numstr] = [
          { 'value': '@integer(1,1000)', 'name': '@integer(1,255).@integer(1,255).@integer(1,255).*' }
        ]
        response.data = Mock.mock(tpl).data.sort((a, b) => {
          if (a.value > b.value) {
            return -1
          }
          if (a.value < b.value) {
            return 1
          }
          return 0
        })
      } else if (target === 'service') {
        response.data = []
      } else if (target === 'tag') {
        response.data = []
      } else if (target === 'finger') {
        response.data = []
      }
      return response
    }
  }
]
