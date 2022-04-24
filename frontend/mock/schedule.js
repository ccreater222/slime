const Mock = require('mockjs')
const mockdata = Mock.mock({
  'data|100': [
    {
      'id|+1': 1,
      'name': '@sentence(5, 10)',
      'cron': '* * * * *',
      'templatetask': '@guid',
      'task|0-10': ['@guid'],
      'nexttime': '2022-04-24',
      'executecount': 0,
      'status': ''
    }
  ]
})
module.exports = [
  {
    url: '/api/schedule',
    type: 'post',
    response: config => {
      let data = []
      const size = config.body.size
      data = mockdata.data.slice(0, size)
      const status = ['schedule', 'pause']
      for (var i = 0; i < data.length; i++) {
        data[i].status = status[Math.floor(Math.random() * status.length)]
        data[i].executecount = data[i].task.length
      }
      return {
        success: true,
        data: {
          columns: Object.keys(data[0]),
          columndatas: data
        },
        total: mockdata.data.length,
        size,
        currentpage: config.body.page,
        page: (mockdata.data.length - mockdata.data.length % config.body.size) / config.body.size
      }
    }
  },
  {
    url: '/api/start/schedule',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  },
  {
    url: '/api/delete/schedule',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  },
  {
    url: '/api/pause/schedule',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  },
  {
    url: '/api/execute/schedule',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  }
]
