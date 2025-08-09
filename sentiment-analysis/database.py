import os
import logging
from pymongo import MongoClient, errors
from datetime import datetime
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        try:
            # Get connection details from environment
            self.mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
            self.database_name = os.getenv('DATABASE_NAME', 'jayadhi')
            
            # Create MongoDB client with connection options
            self.client = MongoClient(
                self.mongodb_uri,
                serverSelectionTimeoutMS=5000,  # 5 second timeout
                retryWrites=True
            )
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Successfully connected to MongoDB: {self.database_name}")
            
            # Get database reference
            self.db = self.client[self.database_name]
            
            # Initialize collections
            self.users = self.db.users
            self.activity_logs = self.db.activity_logs
            self.learning_sessions = self.db.learning_sessions
            self.user_states = self.db.user_states
            
            # Create indexes for performance and data integrity
            self._create_indexes()
            
        except errors.ServerSelectionTimeoutError as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
            raise
    
    def _create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            # Users collection indexes
            self.users.create_index("user_id", unique=True)
            self.users.create_index("created_at")
            
            # Activity logs indexes
            self.activity_logs.create_index([("user_id", 1), ("timestamp", -1)])
            self.activity_logs.create_index("action")
            self.activity_logs.create_index("log_id", unique=True)
            
            # Learning sessions indexes
            self.learning_sessions.create_index("session_id", unique=True)
            self.learning_sessions.create_index([("user_id", 1), ("start_time", -1)])
            self.learning_sessions.create_index("status")
            
            # User states indexes
            self.user_states.create_index("user_id", unique=True)
            self.user_states.create_index("last_updated")
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.warning(f"Index creation failed: {e}")
    
    def log_user_action(self, user_id, action, metadata=None):
        """Log user action with UUID and timestamp"""
        try:
            log_entry = {
                "log_id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "timestamp": datetime.utcnow(),
                "action": action,
                "metadata": metadata or {},
                "session_id": self.get_current_session(user_id)
            }
            result = self.activity_logs.insert_one(log_entry)
            logger.debug(f"Logged action '{action}' for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to log user action: {e}")
            return None
    
    def get_current_session(self, user_id):
        """Get or create current session for user"""
        try:
            # Find active session
            session = self.learning_sessions.find_one(
                {"user_id": str(user_id), "status": "active"},
                sort=[("start_time", -1)]
            )
            
            if session:
                return session["session_id"]
            
            # Create new session
            session_id = str(uuid.uuid4())
            session_doc = {
                "session_id": session_id,
                "user_id": str(user_id),
                "start_time": datetime.utcnow(),
                "status": "active",
                "last_activity": datetime.utcnow()
            }
            
            self.learning_sessions.insert_one(session_doc)
            logger.debug(f"Created new session {session_id} for user {user_id}")
            return session_id
            
        except Exception as e:
            logger.error(f"Failed to get/create session: {e}")
            return str(uuid.uuid4())  # Fallback session ID
    
    def end_session(self, user_id, session_id=None):
        """End current or specified session"""
        try:
            query = {"user_id": str(user_id), "status": "active"}
            if session_id:
                query["session_id"] = session_id
            
            result = self.learning_sessions.update_many(
                query,
                {"$set": {
                    "status": "ended",
                    "end_time": datetime.utcnow()
                }}
            )
            
            logger.debug(f"Ended {result.modified_count} sessions for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to end session: {e}")
            return None
    
    def update_user_state(self, user_id, state_data):
        """Update user journey state"""
        try:
            update_data = {
                **state_data,
                "user_id": str(user_id),
                "last_updated": datetime.utcnow()
            }
            
            result = self.user_states.update_one(
                {"user_id": str(user_id)},
                {"$set": update_data},
                upsert=True
            )
            
            logger.debug(f"Updated state for user {user_id}")
            return result
            
        except Exception as e:
            logger.error(f"Failed to update user state: {e}")
            return None
    
    def get_user_profile(self, user_id):
        """Get comprehensive user profile"""
        try:
            profile = self.users.find_one({"user_id": str(user_id)})
            if profile:
                # Remove MongoDB _id field for cleaner response
                profile.pop("_id", None)
            return profile
            
        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            return {"error": f"User {user_id} not found"}
    
    def create_user_profile(self, user_id, profile_data):
        """Create new user profile"""
        try:
            # Check if user already exists
            existing = self.users.find_one({"user_id": str(user_id)})
            if existing:
                logger.warning(f"User {user_id} already exists")
                return {"error": "User already exists", "user_id": user_id}
            
            # Create profile with defaults
            profile = {
                "user_id": str(user_id),
                "created_at": datetime.utcnow(),
                "name": profile_data.get("name", "Anonymous User"),
                "learning_profile": profile_data.get("learning_profile", "visual"),
                "proficiency_level": profile_data.get("proficiency_level", "beginner"),
                "stress_level": profile_data.get("stress_level", "low"),
                "engagement_level": profile_data.get("engagement_level", "medium"),
                "current_difficulty": profile_data.get("current_difficulty", 3),
                "performance_history": profile_data.get("performance_history", []),
                "sentiment_history": profile_data.get("sentiment_history", []),
                **{k: v for k, v in profile_data.items() if k not in [
                    "name", "learning_profile", "proficiency_level", 
                    "stress_level", "engagement_level", "current_difficulty",
                    "performance_history", "sentiment_history"
                ]}
            }
            
            result = self.users.insert_one(profile)
            logger.info(f"Created profile for user {user_id}")
            
            # Log profile creation
            self.log_user_action(user_id, "profile_created", {
                "name": profile["name"],
                "learning_profile": profile["learning_profile"]
            })
            
            return {"success": True, "user_id": user_id, "inserted_id": str(result.inserted_id)}
            
        except errors.DuplicateKeyError:
            logger.warning(f"Duplicate user creation attempt: {user_id}")
            return {"error": "User already exists", "user_id": user_id}
        except Exception as e:
            logger.error(f"Failed to create user profile: {e}")
            return {"error": f"Profile creation failed: {str(e)}"}
    
    def get_user_activity_summary(self, user_id, limit=100):
        """Get recent user activity summary"""
        try:
            activities = list(self.activity_logs.find(
                {"user_id": str(user_id)},
                {"_id": 0}  # Exclude MongoDB _id
            ).sort("timestamp", -1).limit(limit))
            
            return {
                "user_id": user_id,
                "total_activities": len(activities),
                "recent_activities": activities
            }
            
        except Exception as e:
            logger.error(f"Failed to get activity summary: {e}")
            return {"error": "Failed to retrieve activities"}
    
    def get_database_stats(self):
        """Get database statistics for monitoring"""
        try:
            stats = {
                "database_name": self.database_name,
                "collections": {
                    "users": self.users.count_documents({}),
                    "activity_logs": self.activity_logs.count_documents({}),
                    "learning_sessions": self.learning_sessions.count_documents({}),
                    "user_states": self.user_states.count_documents({})
                },
                "active_sessions": self.learning_sessions.count_documents({"status": "active"}),
                "timestamp": datetime.utcnow()
            }
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get database stats: {e}")
            return {"error": "Stats unavailable"}
    
    def close_connection(self):
        """Close database connection"""
        try:
            self.client.close()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")

# Global database instance with proper error handling
try:
    db = DatabaseManager()
except Exception as e:
    logger.critical(f"Failed to initialize database: {e}")
    # In production, you might want to exit or use a fallback
    raise