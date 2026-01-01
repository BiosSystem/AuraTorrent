import { grey, red } from 'vuetify/util/colors'
import { getVariables } from '@/themes/global'

export default {
  id: 'light-redesigned',
  theme: {
    dark: false,
    colors: {
      primary: '#F0F4F8',
      secondary: '#E2E8F0',
      navbar: '#FFFFFF',
      download: '#0070F3',
      background: '#F8FAFC',
      selected: grey.lighten2,
      red: red.accent2,
      ...getVariables(false),
    },
  },
}
