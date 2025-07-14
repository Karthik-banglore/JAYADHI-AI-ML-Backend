from flask import Flask, request, jsonify
from datetime import datetime
from typing import Dict, List, Any

from personalization_engine import PersonalizationEngine


class TeacherDashboard:
    """
    API endpoints for teacher monitoring and analytics.
    """

    def __init__(self, personalization_engine: PersonalizationEngine):
        self.personalization_engine = personalization_engine

    def get_class_overview(self) -> Dict[str, Any]:
        """Get overview of all students in a class."""
        all_students = self.personalization_engine.student_profiles

        if not all_students:
            return {"message": "No students found", "total_students": 0}

        overview = {
            "total_students": len(all_students),
            "difficulty_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "emotional_summary": {"positive": 0, "neutral": 0, "negative": 0},
            "students_needing_attention": [],
            "timestamp": datetime.now().isoformat()
        }

        for student_id, profile in all_students.items():
            overview["difficulty_distribution"][profile.current_difficulty] += 1

            if profile.sentiment_history:
                recent_sentiments = profile.sentiment_history[-5:]
                negative_count = sum(1 for s in recent_sentiments if s.get('emotion') == 'negative')
                
                if negative_count >= 3:
                    overview["emotional_summary"]["negative"] += 1
                    overview["students_needing_attention"].append({
                        "student_id": student_id,
                        "reason": "Multiple recent negative emotions detected",
                        "difficulty": profile.current_difficulty
                    })
                elif any(s.get('emotion') == 'positive' for s in recent_sentiments):
                     overview["emotional_summary"]["positive"] += 1
                else:
                    overview["emotional_summary"]["neutral"] += 1
            else:
                overview["emotional_summary"]["neutral"] += 1

        return overview

    def get_student_detailed_report(self, student_id: str) -> Dict[str, Any]:
        """Get detailed analytics for a specific student."""
        profile_data = self.personalization_engine.get_profile_data(student_id)

        if "error" in profile_data:
            return {"error": f"Student {student_id} not found"}

        performance_trend = "stable"
        if len(profile_data["performance_history"]) >= 3:
            recent_scores = profile_data["performance_history"][-3:]
            if recent_scores[-1] > recent_scores[0] + 0.1:
                performance_trend = "improving"
            elif recent_scores[-1] < recent_scores[0] - 0.1:
                performance_trend = "declining"

        recommendations = []
        if performance_trend == "declining":
            recommendations.append("Consider reducing difficulty or providing additional support.")
        if profile_data["current_difficulty"] == 1 and performance_trend != "improving":
             recommendations.append("Student may be stuck. Assess if a different teaching approach is needed.")

        return {
            "student_id": student_id,
            "current_status": {
                "difficulty_level": profile_data["current_difficulty"],
                "performance_trend": performance_trend,
            },
            "statistics": {
                "total_assessments": len(profile_data["performance_history"]),
                "average_performance": (sum(p for p in profile_data["performance_history"]) / len(profile_data["performance_history"])) if profile_data["performance_history"] else 0,
            },
            "recommendations": recommendations,
            "raw_data": {
                "performance_history": profile_data["performance_history"],
                "sentiment_history": profile_data["sentiment_history"][-10:] # last 10 sentiments
            },
            "timestamp": datetime.now().isoformat()
        }

    def get_intervention_alerts(self) -> List[Dict[str, Any]]:
        """Get list of students requiring teacher intervention."""
        alerts = []
        for student_id, profile in self.personalization_engine.student_profiles.items():
            alert_reasons = []

            if len(profile.sentiment_history) >= 3:
                if all(s.get('emotion') == 'negative' for s in profile.sentiment_history[-3:]):
                    alert_reasons.append("3 consecutive negative interactions.")

            if len(profile.performance_history) >= 3:
                if all(p < 0.4 for p in profile.performance_history[-3:]):
                    alert_reasons.append("3 consecutive low performance scores (<40%).")

            if alert_reasons:
                alerts.append({
                    "student_id": student_id,
                    "alert_level": "high",
                    "reasons": alert_reasons,
                    "current_difficulty": profile.current_difficulty,
                })
        return alerts

def setup_teacher_dashboard_routes(app: Flask, personalization_engine: PersonalizationEngine, logger):
    """Setup Flask routes for teacher dashboard."""
    dashboard = TeacherDashboard(personalization_engine)

    @app.route('/api/teacher/class-overview', methods=['GET'])
    def class_overview():
        try:
            overview = dashboard.get_class_overview()
            logger.log_api_request('/api/teacher/class-overview', 'GET')
            return jsonify(overview)
        except Exception as e:
            logger.log_error("DashboardError", str(e), endpoint='/api/teacher/class-overview')
            return jsonify({"error": "Could not generate class overview"}), 500

    @app.route('/api/teacher/student/<student_id>', methods=['GET'])
    def student_report(student_id):
        try:
            report = dashboard.get_student_detailed_report(student_id)
            if "error" in report:
                logger.log_api_request('/api/teacher/student', 'GET', student_id, 404)
                return jsonify(report), 404
            logger.log_api_request('/api/teacher/student', 'GET', student_id)
            return jsonify(report)
        except Exception as e:
            logger.log_error("DashboardError", str(e), student_id=student_id, endpoint='/api/teacher/student')
            return jsonify({"error": "Could not generate student report"}), 500

    @app.route('/api/teacher/alerts', methods=['GET'])
    def intervention_alerts():
        try:
            alerts = dashboard.get_intervention_alerts()
            logger.log_api_request('/api/teacher/alerts', 'GET')
            return jsonify({"alerts": alerts, "total_alerts": len(alerts)})
        except Exception as e:
            logger.log_error("DashboardError", str(e), endpoint='/api/teacher/alerts')
            return jsonify({"error": "Could not generate alerts"}), 500