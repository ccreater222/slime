import request from '@/utils/request'
export function getvul(data) {
  return request({
    url: '/api/vuldata',
    method: 'post',
    data
  })
}
