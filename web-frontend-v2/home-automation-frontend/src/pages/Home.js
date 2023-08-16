import React from 'react'
import '../css/general.css'
import MainCard from '../components/CardsAndContainers/MainCard'
import ServerCard from '../components/CardsAndContainers/ServerCard'
import SideBar from '../components/navbars/SideBar'

const Home = () => {

    return (
    <div className='w-100'>
        <SideBar/>
        <div className='container'>
            <div className='w-100 justify-content-center flex-wrap padding-10 margin-10'>
                <MainCard title="Camera's" type='cam' key='camera'/>
            </div>
            <div className='w-100 justify-content-center flex-wrap padding-10 margin-10'>
                <MainCard title="Lock's" type='lock' key='lock'/>
            </div>
            <div className='w-100 justify-content-center flex-wrap padding-10 margin-10'>
                <ServerCard title="Home Servers" type='server' key='server'/>
            </div>
        </div>
    </div>
  )
}

export default Home