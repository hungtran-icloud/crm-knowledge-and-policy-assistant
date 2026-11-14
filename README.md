# SongNhat CRM Knowledge & Policy Assistant

> Trợ lý hỏi đáp nội bộ hỗ trợ nhân viên tra cứu quy trình CRM đã được phê duyệt.
> Câu trả lời có trích dẫn nguồn, phiên bản và tuyến chuyển người có thẩm quyền.

## Kiến trúc

**Modular Monolith + RAG + Policy Control Layer**

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3.12 + FastAPI |
| Frontend | Next.js 14 + TypeScript |
| Database | PostgreSQL 16 + pgvector |
| Storage | S3-compatible (MinIO dev) |
| Cache | Redis (optional) |
| Worker | Celery + Celery Beat |
| Deployment | Docker Compose |

## Cấu trúc thư mục

```
├── backend/        FastAPI app — 12 module nội bộ
├── frontend/       Next.js — Chat Workspace + Evidence Viewer
├── worker/         Celery background jobs
├── data/           CSV templates và sample data
├── docs/           Tài liệu dự án, playbook, work packages
└── infra/          Docker, nginx, scripts hạ tầng
```

## Khởi động nhanh (development)

```bash
cp .env.example .env
docker compose up -d db redis storage
cd backend && pip install -e ".[dev]" && uvicorn src.main:app --reload
```

## Tài liệu

- [Kiến trúc tổng thể](docs/architecture-overview.md)
- [Team Playbook](docs/team-playbook.md)
- [Git Playbook](docs/git-playbook.md)
- [Jira Playbook](docs/jira-playbook.md)
- [Work Packages](docs/work-packages/)

## Cổng nghiệm thu

| Gate | Mô tả |
|---|---|
| G0 | Sẵn sàng xây dựng — xác nhận nguồn, phân quyền, năng lực |
| G1 | Kho kiểm soát ngoại tuyến — import, reconciliation, effective dates |
| G2 | Dùng có giám sát — quality gates, legal review, training |
| G3 | Chấp nhận pilot — 20 ngày làm việc giám sát |
| G4 | Bàn giao — code, tài liệu, đào tạo, restore test |
