import React, { Component } from 'react'
import { Container } from 'reactstrap'

import LeftMessage from './LeftMessage' 
import RightMessage from './RightMessage' 


class ChatArea extends Component {
    scrollToBottom = () => {
        this.messagesEnd.scrollIntoView({ behavior: "smooth" });
    }

    componentDidMount() {
        this.scrollToBottom();
    }
    
    componentDidUpdate() {
        this.scrollToBottom();
    }

    render() {
        const { messages } = this.props
        return (
            <div id="chat-area">
                <Container>
                    {messages.map((message, i) => (
                        message.side === "left" ?
                        <LeftMessage key={i} text={message.text}/> :
                        <RightMessage key={i} text={message.text}/>
                    ))}
                    <div style={{ float:"left", clear: "both" }}
                        ref={(el) => { this.messagesEnd = el;}}>
                    </div>
                </Container>
            </div>
        )
    }
}

export default ChatArea