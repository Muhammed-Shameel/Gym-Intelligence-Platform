export type Member = {
  id: string;
  member_code: string;
  full_name: string;
  email?: string | null;
  phone?: string | null;
  joined_on: string;
  status: string;
  preferred_training_tags: string[];
};

export type MemberListResponse = {
  items: Member[];
  total: number;
};

export type Trainer = {
  id: string;
  trainer_code: string;
  full_name: string;
  skill_tags: string[];
  max_active_members: number;
  active: boolean;
};

export type TrainerListResponse = {
  items: Trainer[];
  total: number;
};
