import request from '@/utils/request'

export function getservice(data) {
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
    url: '/api/service',
    method: 'post',
    data
  })
}
