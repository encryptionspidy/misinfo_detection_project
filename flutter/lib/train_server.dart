
import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:http/http.dart' as http;


class TrainServer extends StatefulWidget {
  const TrainServer({super.key});

  @override
  State<TrainServer> createState() => _TrainServerState();
}

class _TrainServerState extends State<TrainServer> {
  final TextEditingController _controller=TextEditingController();
  final List<Map<String,dynamic>> _message=[];

  void _sendmessage(){
    if(_controller.text.isNotEmpty){
          setState(() {
            _message.add(
              {
                'text':_controller.text,
                'isMe':true
              }
            );
          });
    }
  }


  Future<void> _sendResponse() async {
    final usermessage=_message.last['text'];
    try{
      final response=await http.post(Uri.parse('http://110.172.151.110:8082'),
      headers: {
        'Content-Type':'application/json',
      },
      body:json.encode({
            'message':usermessage,
          }),
      );
      if(response.statusCode==200){
        final responseData=json.decode(response.body);
        final description=responseData['description'];
        final accuracy=responseData['accuracy'];
        final flag_status=responseData['flag_status'];


        setState(() {
          _message.add({
            'description':description,
                'accuracy':accuracy,
                'flag_status':flag_status,
                'isMe':false
          });
        });
      }
      else {
        throw Exception("Failed to connecct server");
      }
    }
    catch(error){
      setState(() {
        _message.add(
          {
            'text':"error",
            'isMe':false
          }
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return const Placeholder();
  }
}
