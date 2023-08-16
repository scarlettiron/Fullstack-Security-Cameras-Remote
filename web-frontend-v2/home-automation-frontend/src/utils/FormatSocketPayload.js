
//correctly formats messages to be sent over websockets
const FormatSocketPayLoad = (dict) => {
    let defaultDict = {
        type:false,
        status:false,
        action:false,
        unit_id:false,
        image:false,
        unit_ip_url:false
    }

    const keys = Object.keys(dict)

    Object.keys(defaultDict).forEach(key => {
        if(keys.includes(key)){
            defaultDict[key] = dict[key]
        }
    })

    return JSON.stringify(defaultDict)
}

export default FormatSocketPayLoad;