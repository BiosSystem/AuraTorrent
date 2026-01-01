import { grey, red } from 'vuetify/util/colors'
import { getVariables } from '@/themes/global'

export default {
  id: 'dark-legacy',
  theme: {
    dark: true,
    colors: {
      primary: '#1A1B2F',
      secondary: '#26294A',
      navbar: '#131426',
      download: '#00F0FF',
      background: '#0F1021',
      selected: grey.darken1,
      red: red.accent3,
      ...getVariables(true),
    },
  },
}
