import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class ChatApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ChatScreen(),
    );
  }
}

class ChatScreen extends StatefulWidget {
  @override
  _ChatScreenState createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  int _responseIndex = 0; // To cycle through responses

  // GlobalKey for accessing the drawer
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  // Function to send a message from "Me"
  void _sendMessage() {
    if (_controller.text.isNotEmpty) {
      setState(() {
        _messages.add({
          'text': _controller.text,
          'isMe': true, // "Me" message
        });
        _controller.clear();  // Clear the text input
      });

      // Simulate a response from AI
      Future.delayed(Duration(milliseconds: 500), _sendAIResponse);
    }
  }

  // Function to send message to Python server and get the response
  Future<void> _sendAIResponse() async {
    final userMessage = _messages.last['text'];

    try {
      final response = await http.post(
        Uri.parse('http://110.172.151.110:8082'),
        headers: {
          'Content-Type': 'application/json',
        },
        body: json.encode({
          'message': userMessage,
        }),
      );

      if (response.statusCode == 200) {
        final responseData = json.decode(response.body);
        final description = responseData['description'];
        final accuracy = responseData['accuracy'];
        final flagStatus = responseData['flag_status'];

        setState(() {
          _messages.add({
            'description': description,
            'accuracy': accuracy,
            'flagStatus': flagStatus,
            'isMe': false, // "Other person" (AI response)
          });
        });
      } else {
        throw Exception('Failed to get response from server');
      }
    } catch (error) {
      setState(() {
        _messages.add({
          'text': 'Error: Could not fetch response from server',
          'isMe': false,
        });
      });
    }
  }

  @override
  void dispose() {
    _controller.dispose();  // Clean up the controller
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,  // Assign the key to the Scaffold
      appBar: AppBar(
        title: Row(
          children: [
            // GestureDetector to detect the tap on the GIF and open the drawer
            GestureDetector(
              onTap: () {
                _scaffoldKey.currentState?.openDrawer();  // Open the drawer when GIF is clicked
              },
              child: SizedBox(
                height: 70,  // Adjust the height of the GIF to fit your design
                width: 70,   // Adjust the width of the GIF to fit your design
                child: Image.asset('images/giphy56-unscreen.gif'),  // Path to your GIF
              ),
            ),
            SizedBox(width: 10),  // Space between GIF and text
            Padding(
              padding: const EdgeInsets.only(top: 8), // Adjust the top padding here
              child: Text(
                'FALO',
                style: TextStyle(
                  color: Colors.blue,
                  fontSize: 23,
                  fontWeight: FontWeight.bold,
                  fontFamily: 'Retrofont',
                ),
              ),
            ),
          ],
        ),
        automaticallyImplyLeading: false, // This hides the default drawer icon in the AppBar
      ),
      drawer: Drawer(
        child: ListView(
          children: <Widget>[
            DrawerHeader(
              decoration: BoxDecoration(
                color: Colors.blue,
              ),
              child: Text(
                'FALO ENGINE',
                style: TextStyle(color: Colors.white, fontSize: 24),
              ),
            ),
            ListTile(
              title: Text('URL CHECKING'),
              onTap: () {},
            ),
            ListTile(
              title: Text('FACT CHECKING'),
              onTap: () {},
            ),
          ],
        ),
      ),
      body: Column(
        children: [
          // Message display area
          Expanded(
            child: ListView.builder(
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isMe = message['isMe'];

                // Render AI-style response for "Other person"
                if (!isMe && message.containsKey('description')) {
                  return _buildAIResponse(message);
                }

                // Render normal message
                return Align(
                  alignment:
                  isMe ? Alignment.centerRight : Alignment.centerLeft,
                  child: Container(
                    margin: const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: isMe ? Colors.blue : Colors.blue,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Text(
                      message['text'],
                      style: TextStyle(
                          color: Colors.white,
                          fontSize: 16),
                    ),
                  ),
                );
              },
            ),
          ),
          // Input and Send Button
          Padding(
            padding: const EdgeInsets.all(18.0),
            child: Row(
              children: [
                Expanded(
                    child: TextField(
                      controller: _controller,  // Ensure the controller is passed
                      decoration: InputDecoration(
                        hintText: "Enter Your Hint",
                        hintStyle: TextStyle(color: Colors.grey),
                        prefixIcon: Icon(
                          Icons.computer,
                          color: Colors.blue,
                        ),
                        suffixIcon: IconButton(
                          onPressed: () {
                            _sendMessage(); // Call _sendMessage properly
                          },
                          icon: const Icon(
                            Icons.send_and_archive_rounded,
                            color: Colors.blue,
                          ),
                        ),
                        // Border when the TextField is inactive (not focused)
                        enabledBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(20),
                          borderSide: BorderSide(color: Colors.blue, width: 2), // Blue border when inactive
                        ),

                        // Border when the TextField is focused (active)
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(20),
                          borderSide: BorderSide(color: Colors.blue, width: 2), // Dark Blue border when active
                        ),
                      ),
                      textInputAction: TextInputAction.send,  // Send message when pressing 'Send' button
                      onSubmitted: (value) {
                        _sendMessage();  // Send message when 'Send' button is pressed
                      },
                    )
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // Widget to build an AI-style response
  Widget _buildAIResponse(Map<String, dynamic> message) {
    return Align(
      alignment: Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 5, horizontal: 10),
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: Colors.blue,
          borderRadius: BorderRadius.circular(10),
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              message['description'],
              style: TextStyle(
                  color: Colors.white,
                  fontSize: 16, fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 10),
            // Progress bar with percentage
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                LinearProgressIndicator(
                  value: double.parse(message['accuracy'].replaceAll('%', '')) / 100, // Progress value (0.0 - 1.0)
                  backgroundColor: Colors.grey.shade400,
                  valueColor: AlwaysStoppedAnimation<Color>(
                      Colors.white),
                ),
                SizedBox(height: 5),
                Text(
                  "Accuracy: ${message['accuracy']}",
                  style: TextStyle(fontSize: 14, color: Colors.white),
                ),
              ],
            ),
            SizedBox(height: 10),
            if (message['flagStatus'] == "Verified")
              Row(
                children: [
                  Icon(Icons.verified, color: Colors.white, size: 18),
                  SizedBox(width: 5),
                  Text(
                    "Verified",
                    style: TextStyle(fontSize: 14, color: Colors.white),
                  ),
                ],
              )
            else
              Row(
                children: [
                  Icon(Icons.warning, color: Colors.white, size: 18),
                  SizedBox(width: 5),
                  Text(
                    "Unverified",
                    style: TextStyle(fontSize: 14, color: Colors.white),
                  ),
                ],
              )
          ],
        ),
      ),
    );
  }
}
