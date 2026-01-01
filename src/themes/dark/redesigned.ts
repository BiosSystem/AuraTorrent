import { grey, red } from 'vuetify/util/colors'
import { getVariables } from '@/themes/global'

export default {
  id: 'dark-redesigned',
  theme: {
    dark: true,
    colors: {
      primary: '#0D1117',
      secondary: '#161B22',
      navbar: '#090D16',
      download: '#00F0FF',
      background: '#05070D',
      selected: grey.darken1,
      red: red.accent3,
      ...getVariables(true),
    },
  },
}
