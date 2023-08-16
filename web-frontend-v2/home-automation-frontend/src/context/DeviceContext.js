import React, {createContext, useContext, useEffect, useState, useCallback} from "react";
import AuthContext from "./AuthContext";
import CustomFetch from '../utils/CustomFetch'
import {deviceUrls} from '../utils/ApiEndpoints'
import { CountRenders } from "../utils/CountRenders";

const DeviceContext = createContext()
export default DeviceContext;

export const DeviceProvider = ({children}) => {
    CountRenders('device context: ')
    const {User} = useContext(AuthContext)
    const {getAllDevices} = deviceUrls
    const [allDevices, setAllDevices] = useState()

    const getUserDevices = useCallback(async () => {
        const fetchConfig = {method:'GET'}
        const {response, data} = await CustomFetch(`${getAllDevices.url}${User.household}`,
         fetchConfig)
         console.log(data)
        if (response.status === 200){
            setAllDevices(data)
            return
        }
        //setTimeout(getUserDevices(), 3000)
        
    }, [User])

    const updateDevices = async () => {
        getUserDevices()
    }


    const removeDeviceCode = (deviceId, codeId) => {
        for(let x = 0; x < allDevices.results.length; x++){
            if(allDevices.results[x].id === deviceId){
                for(let i = 0; x < allDevices.results[x].lock_codes.length; x++){
                    if(allDevices.results[x].lock_codes[i].id === codeId){
                        allDevices.results[x].lock_codes.splice(i,  i + 1)
                        setAllDevices(allDevices)
                        break
                    }
                }
                break
            }
        }
    }

    const addDeviceCode = (code) => {
        const newState = allDevices.results.map(device => {
            if(device.id === code.device){
                const upatedDevice = {lock_codes:[...device.lock_codes, code], ...device}
                console.log(upatedDevice)
                console.log('it equals')
                return upatedDevice
            }
            console.log(device)
            return device
        })
        console.log(newState)
        setAllDevices(oldArray => ({
            results:newState,...oldArray
        }))
        console.log(allDevices)
    }


    const addServertoState = (data) => {
        setAllDevices(oldArray => ({
            servers:[...oldArray.servers, data],
            ...oldArray
        }))
        console.log(allDevices.servers)
    }

    const removeServerFromState = (serverId) => {
        for(let x = 0; x < allDevices.servers.length; x++){
            if(allDevices.servers[x].id === serverId){
                allDevices.servers.splice(x, x + 1)
                setAllDevices(allDevices)
                break
            }
        }
    }

    const deviceData = {
        allDevices:allDevices,
        updateDevices:updateDevices,
        removeDeviceCode:removeDeviceCode,
        addDeviceCode:addDeviceCode,
        removeServerFromState:removeServerFromState,
        addServertoState:addServertoState,

    }

    useEffect(()=>{
        if(!User || allDevices) return
        getUserDevices()
    },[User])

    return (
        <DeviceContext.Provider value={deviceData}>
            {children}
        </DeviceContext.Provider>
    )
}

