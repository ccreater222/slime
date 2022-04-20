import request from '@/utils/request'

export function getresource(data) {
  if (!data.colume) {
    data.colume = []
  }
  if (!data.size) {
    data.size = 20
  }
  if (!data.sort) {
    data.sort = ''
  }
  return request({
    url: '/api/resource',
    method: 'post',
    data
  })
}
