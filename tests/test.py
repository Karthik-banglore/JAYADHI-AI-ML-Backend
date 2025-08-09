"""
MongoDB Atlas Connection Test Script
Run this before deployment to verify your database connection works
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

def test_mongodb_atlas_connection():
    """Test MongoDB Atlas connection and basic operations"""
    try:
        print("✅” Testing MongoDB Atlas Connection...")
        print("-" * 50)
        
        # Get connection details
        mongodb_uri = os.getenv('MONGODB_URI')
        database_name = os.getenv('DATABASE_NAME', 'jayadhi')
        
        if not mongodb_uri:
            print("âŒ MONGODB_URI not found in environment variables")
            print("Make sure your .env file contains:")
            print("MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/...")
            return False
            
        print(f"✅“¡ Connecting to: {database_name}")
        print(f"✅”— URI: {mongodb_uri[:50]}...")
        
        # Test connection
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=10000)
        client.admin.command('ping')
        print("\✅Successfully connected to MongoDB Atlas!")
        
        # Get database
        db = client[database_name]
        
        # Test basic operations
        print(f"\n✅ Testing database operations...")
        
        # Test 1: Create a test document
        test_collection = db.connection_test
        test_doc = {
            "test_id": "atlas_connection_test",
            "timestamp": datetime.utcnow(),
            "status": "success"
        }
        
        result = test_collection.insert_one(test_doc)
        print(f"✅Insert test: Document created with ID {result.inserted_id}")
        
        # Test 2: Read the document
        found_doc = test_collection.find_one({"test_id": "atlas_connection_test"})
        if found_doc:
            print("✅ Read test: Document retrieved successfully")
        
        # Test 3: Update the document
        update_result = test_collection.update_one(
            {"test_id": "atlas_connection_test"},
            {"$set": {"updated_at": datetime.utcnow()}}
        )
        print(f"âœ… Update test: {update_result.modified_count} document updated")
        
        # Test 4: List collections
        collections = db.list_collection_names()
        print(f"âœ… Collections in database: {collections}")
        
        # Test 5: Database stats
        stats = db.command("dbstats")
        print(f"âœ… Database size: {stats.get('dataSize', 0)} bytes")
        
        # Clean up test document
        test_collection.delete_one({"test_id": "atlas_connection_test"})
        print("âœ… Cleanup: Test document removed")
        
        # Close connection
        client.close()
        print("\n✅ All tests passed! Your MongoDB Atlas connection is ready for deployment.")
        return True
        
    except Exception as e:
        print(f" Connection test failed: {str(e)}")
        print("\✅ Troubleshooting tips:")
        print("1. Check your MONGODB_URI in .env file")
        print("2. Verify your MongoDB Atlas credentials")
        print("3. Ensure your IP is whitelisted in Atlas")
        print("4. Check if your cluster is running")
        return False

if __name__ == "__main__":
    test_mongodb_atlas_connection()