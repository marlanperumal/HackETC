import React from "react"

import LeftMessage from './LeftMessage'
import RightMessage from './RightMessage'

const Message = ({text, side="right"}) => (
    <div>
        { side === "right" ?
            <RightMessage text={text}/> :
            <LeftMessage text={text}/>
        }
    </div>
)

export default Message