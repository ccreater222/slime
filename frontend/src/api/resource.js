import request from '@/utils/request'

export function getresource(data) {
  return request({
    url: '/api/resource',
    method: 'post',
    data
  })
}
