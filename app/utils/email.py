import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings


def send_otp_email(recipient_email: str, otp_code: str, recipient_name: str = "User") -> bool:
    """
    Send OTP via email using SMTP (Gmail)
    Configure SMTP_USER and SMTP_PASSWORD in .env file
    """
    try:
        subject = "Welcome to College Digital Voting System - OTP Verification"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    
                    <!-- Welcome Letter Section -->
                    <div style="background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 25px; text-align: center;">
                        <h1 style="margin: 0 0 10px 0; font-size: 28px;">🎉 WELCOME!</h1>
                        <p style="margin: 0; font-size: 16px;">You are now part of the College Digital Voting System</p>
                    </div>
                    
                    <!-- Welcome Message -->
                    <p style="color: #333; font-size: 16px; margin-bottom: 20px;">Hello <strong>{recipient_name}</strong>,</p>
                    
                    <p style="color: #555; line-height: 1.6; margin-bottom: 20px;">
                        Welcome to the <strong>College Digital Voting System</strong>! We are excited to have you on board. 
                        This secure and transparent platform allows you to participate in democratic elections from anywhere, anytime.
                    </p>
                    
                    <!-- Key Features -->
                    <div style="background-color: #f9f9f9; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #2196F3; font-weight: bold; margin: 0 0 10px 0;">✨ Key Features:</p>
                        <ul style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;">🔒 Secure & Encrypted Voting</li>
                            <li style="margin: 8px 0;">📱 Easy-to-Use Interface</li>
                            <li style="margin: 8px 0;">🔐 OTP-Based Authentication</li>
                            <li style="margin: 8px 0;">📊 Real-Time Results</li>
                            <li style="margin: 8px 0;">✅ Transparent & Fair Elections</li>
                        </ul>
                    </div>
                    
                    <!-- OTP Section -->
                    <h2 style="color: #2196F3; margin-top: 30px; margin-bottom: 15px;">Email Verification Required</h2>
                    <p style="color: #333; margin-bottom: 15px;">To complete your registration and access the voting system, please verify your email using the OTP code below:</p>
                    
                    <div style="background-color: #f0f8ff; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <h1 style="color: #2196F3; letter-spacing: 8px; text-align: center; margin: 0; font-size: 32px; font-weight: bold;">{otp_code}</h1>
                    </div>
                    
                    <p style="color: #d32f2f; font-weight: bold; margin: 15px 0;">⏱️ This OTP expires in 10 minutes</p>
                    
                    <!-- Instructions -->
                    <div style="background-color: #fff3e0; border-left: 4px solid #FF9800; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #E65100; margin: 0;"><strong>📋 Next Steps:</strong></p>
                        <ol style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;">Enter the OTP code above on the verification page</li>
                            <li style="margin: 8px 0;">Your email will be verified</li>
                            <li style="margin: 8px 0;">Access the voting dashboard</li>
                            <li style="margin: 8px 0;">Cast your vote securely</li>
                        </ol>
                    </div>
                    
                    <p style="color: #666; margin-bottom: 15px;">
                        <strong>🔐 Security Note:</strong> Never share this OTP with anyone. The College Voting System team will never ask for your OTP via email, phone, or any other means.
                    </p>
                    
                    <!-- Footer -->
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="color: #999; font-size: 12px; margin: 10px 0;">
                            If you didn't create this account, please ignore this email or contact support immediately.
                        </p>
                        <p style="color: #999; font-size: 12px; margin: 10px 0;">
                            For support, contact: <strong>support@collegevoting.edu</strong>
                        </p>
                        <p style="color: #666; margin-top: 15px; margin-bottom: 0;">Best regards,<br><strong>College Digital Voting System Team</strong></p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.SENDER_NAME} <{settings.SENDER_EMAIL}>"
        message["To"] = recipient_email
        
        # Attach HTML version
        message.attach(MIMEText(html_body, "html"))
        
        # Send email via SMTP
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()  # Start TLS encryption
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"\n{'='*60}")
        print(f"[OK] OTP EMAIL SENT SUCCESSFULLY")
        print(f"{'='*60}")
        print(f"To: {recipient_email}")
        print(f"OTP Code: {otp_code}")
        print(f"Valid for: 10 minutes")
        print(f"{'='*60}\n")
        
        return True
        
    except smtplib.SMTPAuthenticationError:
        print(f"[ERROR] SMTP Authentication Failed!")
        print(f"Check your SMTP_USER and SMTP_PASSWORD in .env file")
        print(f"For Gmail, use App Password (not regular password)")
        return False
    except smtplib.SMTPException as e:
        print(f"[ERROR] SMTP Error: {str(e)}")
        return False
    except Exception as e:
        print(f"[ERROR] Error sending email: {str(e)}")
        return False


def send_welcome_email(recipient_email: str, recipient_name: str = "User") -> bool:
    """
    Send a welcome email when user registers
    """
    try:
        subject = "Welcome to College Digital Voting System!"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    
                    <!-- Welcome Header -->
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 25px; text-align: center;">
                        <h1 style="margin: 0 0 10px 0; font-size: 28px;">🎉 WELCOME TO COLLEGE DIGITAL VOTING</h1>
                        <p style="margin: 0; font-size: 14px;">Your account has been successfully created!</p>
                    </div>
                    
                    <!-- Main Content -->
                    <p style="color: #333; font-size: 16px; margin-bottom: 20px;">Hello <strong>{recipient_name}</strong>,</p>
                    
                    <p style="color: #555; line-height: 1.6; margin-bottom: 20px;">
                        Congratulations! Your account in the <strong>College Digital Voting System</strong> has been successfully created. 
                        We are thrilled to have you as part of our democratic platform.
                    </p>
                    
                    <!-- System Overview -->
                    <div style="background-color: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #1976D2; font-weight: bold; margin: 0 0 10px 0;">📚 About Our System:</p>
                        <p style="color: #555; margin: 0; line-height: 1.6;">
                            Our College Digital Voting System is a secure, transparent, and user-friendly platform designed to enable fair and democratic elections. 
                            Every vote counts, and your voice matters.
                        </p>
                    </div>
                    
                    <!-- Key Features -->
                    <div style="background-color: #f9f9f9; border-left: 4px solid #4CAF50; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #4CAF50; font-weight: bold; margin: 0 0 10px 0;">✨ System Features:</p>
                        <ul style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;"><strong>🔒 End-to-End Encryption:</strong> Your vote is secure and confidential</li>
                            <li style="margin: 8px 0;"><strong>📱 Accessible Anytime:</strong> Vote from anywhere, on any device</li>
                            <li style="margin: 8px 0;"><strong>🔐 Two-Factor Authentication:</strong> OTP verification ensures only authorized users vote</li>
                            <li style="margin: 8px 0;"><strong>📊 Real-Time Results:</strong> View election results instantly</li>
                            <li style="margin: 8px 0;"><strong>✅ Transparent Process:</strong> Verifiable and auditable voting system</li>
                            <li style="margin: 8px 0;"><strong>💪 One Vote Per Person:</strong> Advanced anti-fraud mechanisms</li>
                        </ul>
                    </div>
                    
                    <!-- Getting Started -->
                    <div style="background-color: #fff3e0; border-left: 4px solid #FF9800; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #E65100; font-weight: bold; margin: 0 0 10px 0;">🚀 Getting Started:</p>
                        <ol style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;">Log in with your credentials</li>
                            <li style="margin: 8px 0;">Verify your email using OTP</li>
                            <li style="margin: 8px 0;">Complete your profile (if needed)</li>
                            <li style="margin: 8px 0;">View available elections</li>
                            <li style="margin: 8px 0;">Cast your vote securely</li>
                            <li style="margin: 8px 0;">View results in real-time</li>
                        </ol>
                    </div>
                    
                    <!-- Login Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="http://localhost:3000/login" style="display: inline-block; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px;">🔐 Go to Login Page</a>
                    </div>
                    
                    <p style="color: #666; text-align: center; margin: 20px 0;">
                        Or copy this link: <br>
                        <span style="color: #2196F3; font-size: 12px; word-break: break-all;">http://localhost:3000/login</span>
                    </p>
                    
                    <!-- Important Information -->
                    <div style="background-color: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #c62828; font-weight: bold; margin: 0 0 10px 0;">⚠️ Important Reminders:</p>
                        <ul style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;">Never share your password with anyone</li>
                            <li style="margin: 8px 0;">Keep your OTP confidential</li>
                            <li style="margin: 8px 0;">Vote responsibly and honestly</li>
                            <li style="margin: 8px 0;">Report any suspicious activity immediately</li>
                        </ul>
                    </div>
                    
                    <!-- Footer -->
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="color: #555; margin: 10px 0;">
                            If you have any questions or need assistance, please don't hesitate to contact us:
                        </p>
                        <p style="color: #999; font-size: 12px; margin: 10px 0;">
                            <strong>📧 Email:</strong> support@collegevoting.edu<br>
                            <strong>📞 Help Desk:</strong> Available 24/7
                        </p>
                        <p style="color: #666; margin-top: 15px; margin-bottom: 0;">
                            Thank you for being part of our democratic process!<br>
                            <strong>College Digital Voting System Team</strong>
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.SENDER_NAME} <{settings.SENDER_EMAIL}>"
        message["To"] = recipient_email
        
        # Attach HTML version
        message.attach(MIMEText(html_body, "html"))
        
        # Send email via SMTP
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"\n{'='*60}")
        print(f"[OK] WELCOME EMAIL SENT SUCCESSFULLY")
        print(f"{'='*60}")
        print(f"To: {recipient_email}")
        print(f"Recipient: {recipient_name}")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error sending welcome email: {str(e)}")
        return False


def send_login_link_email(recipient_email: str, recipient_name: str, login_url: str) -> bool:
    """
    Send a direct login link via email
    """
    try:
        subject = "Your College Digital Voting System Login Link"
        
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    
                    <!-- Header -->
                    <div style="background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 25px; text-align: center;">
                        <h1 style="margin: 0 0 10px 0; font-size: 28px;">🎉 Welcome to College Digital Voting!</h1>
                        <p style="margin: 0; font-size: 14px;">Your account is ready</p>
                    </div>
                    
                    <!-- Main Message -->
                    <p style="color: #333; font-size: 16px; margin-bottom: 20px;">Hello <strong>{recipient_name}</strong>,</p>
                    
                    <p style="color: #555; line-height: 1.6; margin-bottom: 20px;">
                        Your registration is complete! Click the button below to log in and start voting.
                    </p>
                    
                    <!-- Login Button -->
                    <div style="text-align: center; margin: 30px 0;">
                        <a href="{login_url}" style="display: inline-block; background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%); color: white; padding: 15px 40px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 16px; cursor: pointer;">🔐 Login Now</a>
                    </div>
                    
                    <p style="color: #666; text-align: center; margin: 20px 0;">
                        Or copy this link: <br>
                        <span style="color: #2196F3; font-size: 12px; word-break: break-all;">{login_url}</span>
                    </p>
                    
                    <!-- Important Info -->
                    <div style="background-color: #fff3e0; border-left: 4px solid #FF9800; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #E65100; font-weight: bold; margin: 0 0 10px 0;">⏱️ Link Expiration:</p>
                        <p style="color: #555; margin: 0; line-height: 1.6;">
                            This login link is valid for 24 hours. After that, you'll need to log in with your email and password.
                        </p>
                    </div>
                    
                    <!-- Security Note -->
                    <div style="background-color: #ffebee; border-left: 4px solid #f44336; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #c62828; font-weight: bold; margin: 0 0 10px 0;">🔒 Security:</p>
                        <ul style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;">Do not share this link with anyone</li>
                            <li style="margin: 8px 0;">Only click if you created this account</li>
                            <li style="margin: 8px 0;">If you didn't register, ignore this email</li>
                        </ul>
                    </div>
                    
                    <!-- Getting Started -->
                    <div style="background-color: #e3f2fd; border-left: 4px solid #2196F3; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="color: #1976D2; font-weight: bold; margin: 0 0 10px 0;">🚀 Next Steps After Login:</p>
                        <ol style="color: #555; margin: 10px 0; padding-left: 20px;">
                            <li style="margin: 8px 0;">Verify your email with OTP</li>
                            <li style="margin: 8px 0;">Complete face recognition</li>
                            <li style="margin: 8px 0;">View available elections</li>
                            <li style="margin: 8px 0;">Cast your vote securely</li>
                        </ol>
                    </div>
                    
                    <!-- Footer -->
                    <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                        <p style="color: #555; margin: 10px 0;">
                            Thank you for being part of our democratic process!
                        </p>
                        <p style="color: #999; font-size: 12px; margin: 10px 0;">
                            <strong>📧 Support:</strong> support@collegevoting.edu
                        </p>
                        <p style="color: #666; margin-top: 15px; margin-bottom: 0;">
                            <strong>College Digital Voting System Team</strong>
                        </p>
                    </div>
                </div>
            </body>
        </html>
        """
        
        # Create message
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"{settings.SENDER_NAME} <{settings.SENDER_EMAIL}>"
        message["To"] = recipient_email
        
        # Attach HTML version
        message.attach(MIMEText(html_body, "html"))
        
        # Send email via SMTP
        with smtplib.SMTP(settings.SMTP_SERVER, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        
        print(f"\n{'='*60}")
        print(f"[OK] LOGIN LINK EMAIL SENT SUCCESSFULLY")
        print(f"{'='*60}")
        print(f"To: {recipient_email}")
        print(f"Recipient: {recipient_name}")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error sending login link email: {str(e)}")
        return False
