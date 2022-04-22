
module.exports = [
  {
    'url': '/api/plugins',
    'type': 'get',
    response: config => {
      return {
        'success': true,
        'data': {
          'stage': {
            'info_collect': {
              'display': '信息收集',
              'description': '根据主体名收集信息'
            },
            'topdomain_collect': {
              'display': '主域名收集',
              'description': '根据主体名收集主域名'
            },
            'subdomain_collect': {
              'display': '子域名收集',
              'description': '根据主域名收集子域名'
            },
            'ip_info': {
              'display': 'ip信息收集',
              'description': '根据子域名来获得ip'
            },
            'port_detect': {
              'display': '端口检测',
              'description': '探测ip中存活的端口'
            },
            'service_detect': {
              'display': '服务检测',
              'description': '检测端口上开放的服务信息'
            },
            'fingerprint_detect': {
              'display': '指纹识别',
              'description': '收集指纹'
            },
            'poc_scan': {
              'display': '漏洞扫描',
              'description': '扫描对应端口上服务的漏洞'
            },
            'final_step': {
              'display': '最后一步',
              'description': '最后一步'
            }
          },
          'plugins': {
            'info_collect': [
              {
                'name': 'hackone',
                'required': [
                  'name'
                ],
                'config': [
                  'apikey'
                ]
              },
              {
                'name': 'butian',
                'required': [
                  'name'
                ],
                'config': [
                  'apikey',
                  'scope'
                ]
              }
            ],
            'topdomain_collect': [
              {
                'name': 'hackone',
                'required': [
                  'name'
                ],
                'config': [
                  'apikey'
                ]
              },
              {
                'name': 'butian',
                'required': [
                  'name'
                ],
                'config': [
                  'apikey',
                  'scope'
                ]
              }
            ],
            'subdomain_collect': [
              {
                'name': 'oneforall',
                'required': [
                  'topdomain'
                ],
                'config': [
                  'riskqapi',
                  'proxies'
                ]
              },
              {
                'name': 'ksubdomain',
                'required': [
                  'topdomain'
                ],
                'config': [
                  'dictfile'
                ]
              }
            ],
            'ip_info': [
              {
                'name': 'oneforall',
                'required': [
                  'subdomain'
                ],
                'config': [
                  'riskqapi',
                  'proxies'
                ]
              },
              {
                'name': 'nmap',
                'required': [
                  'subdomain'
                ],
                'config': [
                  'ports',
                  'method'
                ]
              }
            ],
            'port_detect': [
              {
                'name': 'masscan',
                'required': [
                  'ip'
                ],
                'config': [
                  'rate'
                ]
              },
              {
                'name': 'zmap',
                'required': [
                  'ip'
                ],
                'config': [
                  'rate'
                ]
              }
            ],
            'service_detect': [
              {
                'name': 'nmap',
                'required': [
                  'ip',
                  'port'
                ],
                'config': [
                  'ports',
                  'method'
                ]
              }
            ],
            'fingerprint_detect': [
              {
                'name': 'TideFinger',
                'required': [
                  'ip',
                  'port',
                  'service'
                ],
                'config': [
                  'proxy'
                ]
              }
            ],
            'poc_scan': [
              {
                'name': 'nuclei',
                'required': [
                  'ip',
                  'port',
                  'service'
                ],
                'config': [
                  'template'
                ]
              },
              {
                'name': 'fscan',
                'required': [
                  'ip',
                  'port',
                  'service'
                ],
                'config': [
                  'ports'
                ]
              }
            ],
            'final_step': [
              {
                'name': 'xray',
                'required': [

                ],
                'config': [
                  'plugins'
                ]
              }
            ]

          }
        }
      }
    }
  }
]
