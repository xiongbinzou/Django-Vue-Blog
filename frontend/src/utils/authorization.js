import axios from 'axios'

async function authorization() {
  const storage = localStorage
  let hasLogin = false
  let username = storage.getItem('username.myblog')
  const expiredTime = Number(storage.getItem('expiredTime.myblog'))
  const current = (new Date()).getTime()
  const refreshToken = storage.getItem('refresh.myblog')

  if (expiredTime > current) {
    hasLogin = true
    console.log('authorization access')
  } else if (refreshToken !== null) {
    try {
      let response = await axios.post(('/api/token/refresh/', { refresh: refreshToken }))
      const nextExpiredTime = Date.parse(response.headers.date) + 10800000
      storage.setItem('access.myblog', response.data.access)
      storage.setItem('expiredTime.myblog', nextExpiredTime)
      hasLogin = true
      console.log('authorization refresh')
    }
    catch(err) {
      storage.clear()
      hasLogin = false
      console.log('authorization err')
    }
  } else {
    storage.clear()
    hasLogin = false
    console.log('authorization exp')
  }
  console.log('authorization done')
  
  return [hasLogin, username]
}

export default authorization