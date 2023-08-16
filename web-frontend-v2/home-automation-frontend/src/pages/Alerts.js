import React, {useContext, useEffect, useState, useRef} from 'react'
import AuthContext from '../context/AuthContext'
import { alertUrls } from '../utils/ApiEndpoints'
import CustomFetch from '../utils/CustomFetch'
import SideBar from '../components/navbars/SideBar'
import AlertItem from '../components/alerts/AlertItem'
import LoadingSpinner1 from '../components/loadingAndErrors/LoadingSpinner1'

const Alerts = () => {
    const {User} = useContext(AuthContext)
    const [loading, setLoading] = useState(true)

    const {getAllAlerts} = alertUrls

    const [alerts, setAlerts] = useState(null)

    const observer = useRef()

    const fetchAllAlerts = async () => {
        console.log('fetching alerts')
        const fetchConfig = {method:'GET'}
        const {response, data} = await CustomFetch(`${getAllAlerts.url}${User.household}/`, fetchConfig)

        if(response.status === 200){
            setAlerts(data)
            setLoading(false)
        } 

    }

    const handlePagination = async () => {
        if(!alerts.next) return
        setLoading(true)
        const fetchConfig = {method:'GET'}
        const {response, data} = await CustomFetch(alerts.next, fetchConfig)

        if(response.status === 200){
            setAlerts(oldArray => ({results:[...oldArray.results, data.results], count:data.count,
            previous:data.previous, next:data.next}))
        }
        setLoading(false)
    }

    const handleTrackPosition = element => {
        if(!alerts.next) return
        if(observer.current) {observer.current.disconnect()}
        observer.current = new IntersectionObserver(entries => {
          if(entries[0].isIntersecting){
            handlePagination()
          }
        })
        if(element) {observer.current.observe(element)}
      }
 
    useEffect(() => {
        fetchAllAlerts()
    }, [])
 
    return (
    <div className='w-100'>
        <SideBar/>
        <div className='container'>

            {alerts && alerts.count > 0 &&
                alerts.results.map((alert, index) => {
                    if(index === alerts.results.length - 1 && alerts.next){
                        return <>
                                    <AlertItem alert = {alert} key={index}/>
                                    <div ref={handleTrackPosition} />
                                </>
                    }
                    else{
                        return <AlertItem alert = {alert} key={index}/>
                    }
                })
            }
            {
                loading && 
                <LoadingSpinner1/>
            }
        </div>
    </div>
  )
}

export default Alerts