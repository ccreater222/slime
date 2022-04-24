import request from '@/utils/request'
export function getschedule(data) {
  return request({
    url: '/api/schedule',
    method: 'post',
    data
  })
}
export function actionschedule(action, data) {
  return request({
    url: `/api/${action}/schedule`,
    method: 'post',
    data
  })
}
