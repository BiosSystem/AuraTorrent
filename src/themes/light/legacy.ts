import { grey, red } from 'vuetify/util/colors'
import { getVariables } from '@/themes/global'

export default {
  id: 'light-legacy',
  theme: {
    dark: false,
    colors: {
      primary: '#E6ECF5',
      secondary: '#D9E2EC',
      navbar: '#F0F4F8',
      download: '#0070F3',
      background: '#F4F7FA',
      selected: grey.lighten2,
      red: red.accent2,
      ...getVariables(false),
    },
  },
}
