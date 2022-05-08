import request from '@/utils/request'

export function createtask(data) {
  return request({
    url: '/api/create/task',
    method: 'post',
    data
  })
}
export function gettask(data) {
  if (!data.columns) {
    data.columns = []
  }
  if (!data.size) {
    data.size = 20
  }
  if (!data.sort) {
    data.sort = ''
  }
  return request({
    url: '/api/task',
    method: 'post',
    data
  })
}
export function actiontask(action, data) {
  return request({
    url: `/api/${action}/task`,
    method: 'post',
    data
  })
}
