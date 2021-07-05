import { useEffect } from "react"
import { navigate } from "@reach/router"

const IndexPage = () => {
  useEffect(() => {
    navigate("/start/")
  }, [])
  return null
}
export default IndexPage
