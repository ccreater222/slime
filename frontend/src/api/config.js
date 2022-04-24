import request from '@/utils/request'
export function getconfig(data) {
  return request({
    url: '/api/config',
    method: 'post',
    data
  })
}
export function saveconfig(data) {
  return request({
    url: '/api/save/config',
    method: 'post',
    data
  })
}
