
import { useRef } from "react"

export const CountRenders = (prop = ' ') => {
    const count = useRef(1)
    console.log(` ${prop} number of renders: ${count.current++}`)
}