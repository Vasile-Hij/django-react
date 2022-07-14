import React, {useContext} from 'react'
import AuthContext from '../context/AuthContext'

const LoginPage = () => {
    let {registerUser} = useContext(AuthContext)
    return (
        <div>
            <form onSubmit={loginUser}>
                <input type="text" name="username" placeholder="Enter Username" />
                <input type="password" name="password" placeholder="Enter Password" />
                <input type="submit"/>
            </form>
        </div>
    )
}

export default LoginPage;