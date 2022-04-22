import request from '@/utils/request'

export function createtask(data) {
  return request({
    url: '/api/create/task',
    method: 'post',
    data
  })
}
