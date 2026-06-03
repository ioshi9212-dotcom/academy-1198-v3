# Placeholder for ApplyTurnResultSimple endpoint implementation
# This file will contain the new endpoint that GPT Actions can use to send JSON strings instead of object fields.
# The structure follows the earlier plan:
# - ApplyTurnResultSimpleRequest BaseModel
# - parse_json_text function
# - /api/v1/sessions/{session_id}/apply-turn-result-simple POST endpoint
# - Calls existing apply_turn_result internally