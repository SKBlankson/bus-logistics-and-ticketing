
class User {
  int? userId;
  String? name;
  String? email;
  String? phone;
  

  User({
    this.userId,
     this.name, 
     this.email, 
     this.phone
    }
  );

  factory User.fromJson(Map<String, dynamic> responseData) {
    return User(
        userId: responseData['id'],
        name: responseData['name'],
        email: responseData['email'],
        phone: responseData['phone'],
       
    );
  }
}