const convertToFormattedSiteDate = (date) => {
    let newDateObj = new Date(date)
    return newDateObj.toDateString()
}

const convertToFormattedSiteTime = (data) => {
    let newDateObj = new Date(data)
    let localDate = newDateObj.toLocaleTimeString([], {hour:'2-digit', minute:'2-digit', hour12:true})
    return localDate
} 

export {convertToFormattedSiteDate, convertToFormattedSiteTime}