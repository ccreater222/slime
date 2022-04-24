const Mock = require('mockjs')
const plugins = {
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
var mocktpl = {}
Object.keys(plugins).forEach(stage => {
  plugins[stage].forEach(plugin => {
    plugin.config.forEach(config => {
      if (mocktpl[stage] === undefined) {
        mocktpl[stage] = {}
      }
      if (mocktpl[stage][plugin.name] === undefined) {
        mocktpl[stage][plugin.name] = {}
      }
      mocktpl[stage][plugin.name][config] = '@sentence(10,20)'
    })
  })
})
const mockdata = Mock.mock({
  data: {
    plugins: mocktpl,
    global: {
      'proxies': 'http://127.0.0.1:1080'
    }
  }
})
module.exports = [
  {
    url: '/api/config',
    type: 'post',
    response: config => {
      return {
        success: true,
        data: mockdata.data
      }
    }
  },
  {
    url: '/api/save/config',
    type: 'post',
    response: config => {
      return {
        success: true
      }
    }
  }
]
