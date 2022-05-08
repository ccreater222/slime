import request from '@/utils/request'

export function getresource(data) {
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
    url: '/api/resource',
    method: 'post',
    data
  })
}
export function updateresource(data) {
  return request({
    url: '/api/update/resource',
    method: 'post',
    data
  })
}
export function createresource(data) {
  return request({
    url: '/api/create/resource',
    method: 'post',
    data: {
      data
    }
  })
}
export function deleteresource(data) {
  return request({
    url: '/api/delete/resource',
    method: 'post',
    data
  })
}
export function analyzeresource(data) {
  return request({
    url: '/api/analyze/resource',
    method: 'post',
    data
  })
}
