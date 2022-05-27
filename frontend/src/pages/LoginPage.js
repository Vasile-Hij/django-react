import React , {useContext} from 'react'
import AuthContext from '../context/AuthContext'

const LoginPage = () => {
  let {loginUser} = useContext(AuthContext)
  return (
    <div>
        <form onSubmit={loginUser}>
            <input type="text" name='username' pacleholder="Enter username"></input>
            <input type="text" name='password' pacleholder="Enter password"></input>
            <input type="submit"></input>
        </form>
    </div>
  )
}

export default LoginPage