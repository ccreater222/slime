import request from '@/utils/request'

export function getplugins() {
  return request({
    url: '/api/plugins',
    method: 'get'
  })
}
