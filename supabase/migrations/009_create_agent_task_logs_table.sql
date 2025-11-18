-- Create agent_task_logs table
CREATE TABLE IF NOT EXISTS agent_task_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    agent_name VARCHAR(100) NOT NULL,
    task_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) NOT NULL,
    input_data JSONB,
    output_data JSONB,
    error_message TEXT,
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_agent_task_logs_agent_name ON agent_task_logs(agent_name);
CREATE INDEX IF NOT EXISTS idx_agent_task_logs_status ON agent_task_logs(status);

