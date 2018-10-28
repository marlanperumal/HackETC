import React, { Component } from 'react'
import './App.css'

import Header from './components/Header'
import ChatArea from './components/ChatArea'
import Footer from './components/Footer'

import { library } from '@fortawesome/fontawesome-svg-core'
import { faArrowAltCircleRight } from '@fortawesome/free-solid-svg-icons'
import { faCreativeCommonsBy } from '@fortawesome/free-brands-svg-icons'

library.add(faArrowAltCircleRight)
library.add(faCreativeCommonsBy)

// const demo_messages = [
//     {side: "right", text: "I need to go from here to 23 Vilakazi Street on public transport"},
//     {side: "left", text: "I see you're currently at Cresta Shopping Center, Randburg. Do you want the quickest or the cheapest route"},
//     {side: "right", text: "Cheapest"},
//     {side: "left", text: "When do you want to leave or arrive?"},
//     {side: "right", text: "Leave now"},
//     {side: "left", text: "Great, there's taxi and then a bus you can take"},
//     {side: "left", text: "If you leave now, you shoould arrive at 18:04"},
//     {side: "left", text: "Do you want a map or directions?"},
//     {side: "right", text: "Directions"},
//     {side: "left", text: "There's a taxi rank nearby at Cresta Shopping Center. Taxi a taxi towards Bree Taxi Rank. Get off at Enoch Sontonga Avenue near Yale Road."},
//     {side: "right", text: "I got off the taxi"},
//     {side: "left", text: "Walk to Park Station"},
//     {side: "left", text: "..."},
//     {side: "left", text: "Turn right onto Smit Street, M10 and head west"},
//     {side: "left", text: "Then you will arrive at Park Station"},
//     {side: "right", text: "I'm at the station"},
//     {side: "left", text: "Take the Metrorail train from Johannesburg to Naledi and get off at the Phefeni Train Station"},
//     {side: "right", text: "I got off the train"},
//     {side: "left", text: "It's a 10 min walk to your destination from here"},
//     {side: "left", text: "Head southwest on Twala Street"},
//     {side: "left", text: "..."},
//     {side: "left", text: "Turn sharp right onto Moema Street and head southwest"},
//     {side: "left", text: "Then you will arrive at your destination"},
//     {side: "right", text: "Thanks UDrive!"},
//     {side: "left", text: "You're welcome 😊"},
// ]

class App extends Component {
    constructor(props) {
        super(props)
        this.state = {
            messages: [
                {
                    side: "left",
                    text: "Hi James - I'm UDrive! Where would you like to go today?"
                },
                // ...demo_messages
            ],
            origin: "",
            destination: "",
            priority: "cost",
            leave_time: "now",
            arrive_time: null,
            legs: [],
            current_leg: 0,
            typing: false
        }
    }

    getReply = (message) => {
        const { origin, destination, priority, leave_time, arrive_time, legs, current_leg } = this.state
        const data = {
            message, origin, destination, priority, leave_time, arrive_time, legs, current_leg
        }
        return fetch('http://localhost:5000/message', {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, cors, *same-origin
            cache: "no-cache", // *default, no-cache, reload, force-cache, only-if-cached
            credentials: "same-origin", // include, same-origin, *omit
            headers: {
                "Content-Type": "application/json; charset=utf-8",
                // "Content-Type": "application/x-www-form-urlencoded",
            },
            redirect: "follow", // manual, *follow, error
            referrer: "no-referrer", // no-referrer, *client
            body: JSON.stringify(data), // body data type must match "Content-Type" header
        })
        .then(response => response.json())
    }

    sendMessage = (text) => {
        this.addMessage("right", text)
        this.setState({"typing": true})
        this.getReply(text)
        .then(response => {
            console.log(response)
            this.setState({
                ...response,
                messages: [
                    ...this.state.messages,
                    ...response.reply.map(msg => ({
                        side: "left",
                        text: msg
                    }))
                ],
                typing: false
            })    
        })
    }

    addMessage = (side, text) => {
        this.setState({
            messages: [
                ...this.state.messages,
                {
                    side,
                    text
                }
            ]
        })
    }

    render() {
        return (
            <div className="App">
                <Header/>
                <ChatArea messages={this.state.messages} typing={this.state.typing} />
                <Footer onSubmit={this.sendMessage}/>
            </div>
        );
    }
}

export default App
