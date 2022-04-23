const Mock = require('mockjs')
var mockdata = Mock.mock(
  {
    'data|100': [
      {
        'taskid': '@guid',
        'stageinfo': {
          'topdomain_collect': [
            {
              'name': 'butian',
              'config': {
                'apikey': 'aaaaaaa',
                'scope': 'bbbbbbbb'
              }
            }
          ],
          'subdomain_collect': [
            {
              'name': 'oneforall',
              'config': {
                'riskqapi': 'asdfasdfasdf',
                'proxies': 'http://127.0.0.1:1080'
              }
            }
          ]
        },
        'status': 'done', // done wait execute failed
        'log': {
          'topdomain_collect': {
            'butian': '@sentence(100,1000)'
          },
          'subdomain_collect': {
            'oneforall': '@sentence(100,1000)'
          }
        },
        'columns': ['id', 'name', 'topdomain', 'subdomain', 'iscdn', 'ip', 'port', 'service', 'tag', 'finger', 'updated', 'taskid'],
        'page': 10,
        'size': 50,
        'sort': '',
        'desc': false,
        'condition': {},
        'selectall': false,
        'selected': [],
        'created': '@datetime'
      }
    ]
  }
)
module.exports = [
  {
    'url': '/api/create/task',
    'type': 'post',
    'response': config => {
      return {
        success: true
      }
    }
  },
  {
    'url': '/api/task',
    'type': 'post',
    'response': config => {
      let data = []
      const size = config.body.size
      data = mockdata.data.slice(0, size)
      const status = ['done', 'wait', 'execute', 'failed']
      for (var i = 0; i < data.length; i++) {
        data[i].status = status[Math.floor(Math.random() * status.length)]
      }
      return {
        success: true,
        data: {
          tasklist: data,
          total: mockdata.data.length,
          size: config.body.size,
          taskcolumn: ['taskid', 'stageinfo', 'status', 'log', 'created'],
          currentpage: config.body.currentpage,
          page: (mockdata.data.length - mockdata.data.length % config.body.size) / config.body.size
        }
      }
    }
  },
  {
    url: '/api/start/task',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  },
  {
    url: '/api/stop/task',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  },
  {
    url: '/api/pause/task',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  },
  {
    url: '/api/restart/task',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  }
]
