import request from '@/utils/request'
export function getdashboard() {
  return request({
    url: '/api/dashboard',
    method: 'get'
  })
}
